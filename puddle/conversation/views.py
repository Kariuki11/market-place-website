from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from item.models import Item

from .forms import ConversationMessageForm
from .models import Conversation

@login_required
def new_conversation(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)
    
    if item.created_by == request.user:
        return redirect('dashboard:index')
    
    conversations = Conversation.objects.filter(item=item).filter(members__in=[request.user.id])
    
    if conversations:
        pass  # Return to conversations
    
    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)
        
        if form.is_valid():
            conversation = Conversation.objects.create(item=item)
            conversation.members.add(request.user)
            conversation.members.add(item.created_by)
            conversation.save()
            
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()
            
            return redirect('item:detail', pk=item_pk)
    else:
        form = ConversationMessageForm()  # This should be initialized outside the POST block

    return render(request, 'conversation/new.html', {  # This return should be outside the if-else
        'form': form,
    })
    
@login_required
def inbox(request):
    conversations = Conversation.objects.filter(members__in=[request.user.id])
    
    return render(request, 'conversation/inbox.html', {
        'conversations': conversations,
    })
    
@login_required
def detail(request, pk):
    # Retrieve the conversation or return a 404 error if not found
    conversation = get_object_or_404(Conversation, pk=pk, members__in=[request.user.id])
    
    # Render the template with the conversation instance
    return render(request, 'conversation/detail.html', {
        'conversation': conversation
    })


# @login_required
# def detail(request, pk):
#     conversations = Conversation.objects.filter(members__in=[request.user.id]).get(pk=pk)
    
#     return render(request, 'conversation/detail.html', {
#         'conversation': Conversation
#     })
    



# from django.shortcuts import render, get_object_or_404, redirect

# from item.models import Item

# from .forms import ConversationMessageForm
# from .models import Conversation

# def new_conversation(request, item_pk):
#     item = get_object_or_404(Item, pk=item_pk)
    
#     if item.created_by == request.user:
#         return redirect('dashboard:index')
    
#     conversations = Conversation.objects.filter(item=item).filter(members__in=[request.user.id])
    
#     if conversations:
#         pass # Return to conversations
    
#     if request.method == 'POST':
#         form = ConversationMessageForm(request.POST)
        
#         if form.is_valid():
#             conversation = Conversation.objects.create(item=item)
#             conversation.members.add(request.user)
#             conversation.members.add(item.created_by)
#             conversation.save()
            
#             conversation_message = form.save(commit=False)
#             conversation_message.conversation = conversation
#             conversation_message.created_by = request.user
#             conversation_message.save()
            
#             return redirect('item:detail', pk=item_pk)
        
#         else:
#             form = ConversationMessageForm()
            
#         return render(request, 'conversation/new.html',{
#             'form': form,
#         })
        
