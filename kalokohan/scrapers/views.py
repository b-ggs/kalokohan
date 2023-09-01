import facebook_scraper as fs
from django.http import HttpResponse
from django.views.generic import View


class CGPinnedPostView(View):
    POST_ID = "2440831399461869"

    def get(self, request, *args, **kwargs):
        generator = fs.get_posts(post_urls=iter([self.POST_ID]))

        post = next(generator)

        text = post["text"]

        return HttpResponse(text, content_type="text/plain")
