from blog.forms import CommentForm, ContactForm, EmailBlogForm, RegisterForm
from blog.models import Blog, Comment

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render

from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, DeleteView, FormView, ListView, UpdateView

User = get_user_model()


def index(request):
    return render(request, '*')


class RegisterFormView(SuccessMessageMixin, FormView):
    template_name = '*'
    form_class = RegisterForm
    success_url = reverse_lazy('blog:index')
    success_message = 'Profile created'

    def form_valid(self, form):
        form.save()

        username = self.request.POST['username']
        password = self.request.POST['password1']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        send_mail(subject='Welcome to my BLOG', message=f'Hi {username}, thank you for registering in my Blog.',
                  from_email=settings.EMAIL_HOST_USER, recipient_list=['random@example.com'], fail_silently=True)

        return super(RegisterFormView, self).form_valid(form)


class UpdateProfile(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email']
    template_name = '*'
    success_message = 'Profile updated'

    def get_success_url(self):
        return reverse('blog:user-detail', kwargs={'pk': self.object.pk})

    def get_object(self, queryset=None):
        user = self.request.user
        return user


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ['title', 'short_description', 'image', 'full_description', 'posted']
    template_name = '*'
    success_url = reverse_lazy('blog:post-list')
    success_message = 'Post created'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()

        send_mail(subject='New post', message=f'New {post} created! Check it on admin panel.',
                  from_email=settings.EMAIL_HOST_USER,
                  recipient_list=['admin@example.com'],
                  fail_silently=True)
        self.object = post
        return HttpResponseRedirect(self.get_success_url())


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    fields = ['title', 'short_description', 'image', 'full_description', 'posted']
    success_url = reverse_lazy('blog:post-list')
    template_name = '*'
    login_url = reverse_lazy('login')


class PostDeleteView(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('blog:index')
    model = Blog
    success_url = reverse_lazy('blog:post-list')
    template_name = '*'


@method_decorator(cache_page(20), name='dispatch')
class PostListView(generic.ListView):
    model = Blog
    paginate_by = 5
    template_name = '*'
    context_object_name = 'posts'

    def get_queryset(self):
        return Blog.objects.all().filter(posted=True)


def post_detail(request, pk):
    post = get_object_or_404(Blog, pk=pk, posted=True)
    comments = post.comments.filter(active=True)

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            messages.success(request, 'Successful! Sent')
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return HttpResponseRedirect(reverse('blog:post-detail', args=(post.id,)))
    else:
        comment_form = CommentForm()

    return render(request, '*',
                  {'post': post, 'comments': comments, 'comment_form': comment_form})


class UserListView(ListView):
    model = User

    template_name = '*'
    paginate_by = 10

    def get_queryset(self):
        return User.objects.filter(is_staff=False)


class UserDetailView(generic.ListView):
    model = Blog
    paginate_by = 5
    template_name = '*'
    success_message = 'Profile Updated'

    def get_queryset(self):
        id = self.kwargs['pk']
        target_user = get_object_or_404(User, pk=id)
        return Blog.objects.filter(user=target_user)

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context['users'] = get_object_or_404(User, pk=self.kwargs['pk'])
        return context


def reply_page(request):
    if request.method == "POST":

        form = CommentForm(request.POST)

        if form.is_valid():
            post_id = request.POST.get('post_id')
            parent_id = request.POST.get('parent')
            post_url = request.POST.get('post_url')
            messages.success(request, 'Successful! Sent')
            print(post_id)
            print(parent_id)
            print(post_url)

            reply = form.save(commit=False)

            reply.post = Blog(id=post_id)
            reply.parent = Comment(id=parent_id)
            reply.save()

            return HttpResponseRedirect(reverse('blog:post-detail', args=(post_id,)))

    return redirect("/")




def post_share(request, post_id):
    post = get_object_or_404(Blog, id=post_id)
    sent = False

    if request.method == 'POST':

        form = EmailBlogForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True

    else:
        form = EmailBlogForm()
    return render(request, '*', {'post': post,
                                               'form': form,
                                               'sent': sent})
