from django.http import Http404

class IsPostAuthorMixin(object):
    def get_object(self, *args, **kwargs):
        instance = super(IsPostAuthorMixin, self).get_object(*args, **kwargs)
        if not instance.author == self.request.user:
            raise Http404
        return instance
    
class IsCommentAuthorMixin(object):
    def get_object(self, *args, **kwargs):
        instance = super(IsCommentAuthorMixin, self).get_object(*args, **kwargs)
        if not instance.comment_author == self.request.user:
            raise Http404
        return instance