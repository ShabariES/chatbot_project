from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, StreamingHttpResponse
from django.conf import settings
from django.views.decorators.http import require_POST
from groq import Groq
import json
from .models import Conversation, ChatMessage

SYSTEM_PROMPT = (
    "You are NewTurn, an elite AI assistant and expert coding companion — powered by Groq. "
    "Your responses must be articulate, accurate, complete, and beautifully formatted using standard Markdown.\n\n"
    "CODE FORMATTING & OUTPUT RULES:\n"
    "1. Whenever writing code, ALWAYS enclose code in fenced code blocks with the exact language specified immediately after opening triple backticks (e.g. ```python, ```javascript, ```html, ```css, ```sql, ```bash, ```json, ```cpp).\n"
    "2. Provide complete, clean, production-ready, fully commented, and runnable code. NEVER use placeholders or shortcuts like '// add rest of code here' or '...'.\n"
    "3. Structure your response with bold subheadings, bullet points, concise step-by-step instructions, and proper code block structure.\n"
    "4. Be warm, professional, thorough, and clear."
)


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('chat_home')
    else:
        form = UserCreationForm()
    return render(request, 'chat/signup.html', {'form': form})


@login_required
def chat_home(request):
    return render(request, 'chat/chat.html')


@login_required
def list_conversations(request):
    """Returns JSON list of conversations for the logged-in user."""
    convs = Conversation.objects.filter(user=request.user)
    data = [
        {
            'id': c.id,
            'title': c.title,
            'updated_at': c.updated_at.strftime('%b %d, %H:%M') if c.updated_at else ''
        }
        for c in convs
    ]
    return JsonResponse({'conversations': data})


@login_required
def get_conversation_messages(request, conversation_id):
    """Returns JSON messages for a given conversation."""
    conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
    messages = conversation.messages.all()
    data = [
        {
            'id': m.id,
            'sender': m.sender,
            'content': m.content,
            'timestamp': m.timestamp.strftime('%H:%M') if m.timestamp else ''
        }
        for m in messages
    ]
    return JsonResponse({
        'conversation_id': conversation.id,
        'title': conversation.title,
        'messages': data
    })


@login_required
@require_POST
def delete_conversation(request, conversation_id):
    """Deletes a user's conversation."""
    conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
    conversation.delete()
    return JsonResponse({'status': 'ok'})


@login_required
def stream_bot_response(request):
    """
    Streams the Groq reply as Server-Sent Events (SSE) and saves to database.
    """
    user_message = request.GET.get('msg', '').strip()
    conv_id = request.GET.get('conversation_id', '').strip()

    if not user_message:
        def _empty():
            yield 'data: {"done": true}\n\n'
        return StreamingHttpResponse(_empty(), content_type='text/event-stream')

    # Get or create conversation
    conversation = None
    if conv_id and conv_id.isdigit():
        conversation = Conversation.objects.filter(id=int(conv_id), user=request.user).first()

    if not conversation:
        title = user_message[:36].strip()
        if len(user_message) > 36:
            title += '…'
        conversation = Conversation.objects.create(user=request.user, title=title)

    # Save user message to database
    ChatMessage.objects.create(
        conversation=conversation,
        sender='user',
        content=user_message
    )

    # Fetch recent history (up to last 20 messages) for API context
    recent_msgs = list(conversation.messages.all().order_by('-timestamp')[:20])
    recent_msgs.reverse()

    history = [{'role': m.sender, 'content': m.content} for m in recent_msgs]
    messages = [{'role': 'system', 'content': SYSTEM_PROMPT}] + history

    def event_stream():
        full_reply = ''
        # Initial chunk sending conversation metadata
        meta = json.dumps({"conversation_id": conversation.id, "title": conversation.title})
        yield f'data: {meta}\n\n'

        try:
            client = Groq(api_key=settings.GROQ_API_KEY)
            model_name = getattr(settings, 'GROQ_MODEL', 'groq/compound')
            stream = client.chat.completions.create(
                model=model_name,
                messages=messages,
                temperature=0.7,
                max_tokens=2048,
                stream=True,
            )
            for chunk in stream:
                delta = chunk.choices[0].delta.content
                if delta:
                    full_reply += delta
                    yield f'data: {json.dumps({"token": delta})}\n\n'

        except Exception as exc:
            yield f'data: {json.dumps({"error": str(exc)})}\n\n'

        # Save assistant message to database if reply exists
        if full_reply:
            ChatMessage.objects.create(
                conversation=conversation,
                sender='assistant',
                content=full_reply
            )
            conversation.save() # Updates updated_at timestamp

        yield f'data: {json.dumps({"done": True})}\n\n'

    response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'
    return response


@login_required
def clear_chat_history(request):
    """Resets Groq conversation context in session if used."""
    return JsonResponse({'status': 'ok'})