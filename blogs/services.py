from typing import Protocol, OrderedDict
from blogs import repos

class PostListCreateServiceInterface(Protocol):
    def create_post(self, data: OrderedDict): ...

    def get_posts(self, data: OrderedDict): ...


class PostGetUpdateDeleteServiceInterface(Protocol):
    def get_post(self, pk: int): ...

    def like_post(self, post_id, user): ...


class CommentListCreateServiceInterface(Protocol):
    def get_comments(self, post_id: int): ...

    def create_comment(self, post_id: int, data: OrderedDict): ...

class PostListCreateServiceV1:
    post_repos: repos.PostListCreateReposInterface = repos.PostListCreateReposV1()

    def create_post(self, data: OrderedDict):
        return self.post_repos.create_post(data=data)

    def get_posts(self):
        return self.post_repos.get_posts()


class PostGetUpdateDeleteServiceV1:
    post_repos: repos.PostGetUpdateDeleteReposInterface = repos.PostGetUpdateDeleteReposV1()

    def get_post(self, pk: int):
        return self.post_repos.get_post(pk=pk)

    def like_post(self, post_id, user):
        return self.post_repos.like_post(post_id=post_id, user=user)


class CommentListCreateServiceV1:
    comment_repos: repos.CommentListCreateReposeInterface = repos.CommentListCreateReposV1()

    def get_comments(self, post_id: int):
        return self.comment_repos.get_comments(post_id=post_id)

    def create_comment(self, post_id: int, data: OrderedDict):
        return self.comment_repos.create_comment(post_id=post_id, data=data)
