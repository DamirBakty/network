import logging
from typing import Protocol, OrderedDict

from blogs.repos.posts import PostListCreateReposInterface, PostListCreateReposV1, PostGetUpdateDeleteReposInterface, \
    PostGetUpdateDeleteReposV1


logger = logging.getLogger(__name__)


class PostListCreateServiceInterface(Protocol):
    def create_post(self, data: OrderedDict): ...

    def get_posts(self, data: OrderedDict): ...


class PostGetUpdateDeleteServiceInterface(Protocol):
    def get_post(self, pk: int, user=None): ...

    def like_post(self, post_id, user): ...

    def mark_post(self, post_id, user): ...


class PostListCreateServiceV1:
    post_repos: PostListCreateReposInterface = PostListCreateReposV1()

    def create_post(self, data: OrderedDict):
        return self.post_repos.create_post(data=data)

    def get_posts(self):
        return self.post_repos.get_posts()


class PostGetUpdateDeleteServiceV1:
    post_repos: PostGetUpdateDeleteReposInterface = PostGetUpdateDeleteReposV1()

    def get_post(self, pk: int, user=None):
        return self.post_repos.get_post(pk=pk, user=user)

    def like_post(self, post_id, user):
        logger.debug(f'Post with id {post_id} is liked')

        return self.post_repos.like_post(post_id=post_id, user=user)

    def mark_post(self, post_id, user):
        return self.post_repos.mark_post(post_id, user)
