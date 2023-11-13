from typing import Protocol, OrderedDict

from blogs.repos.comments import CommentListCreateReposInterface, CommentListCreateReposV1, \
    CommentGetUpdateDeleteReposInterface, CommentGetUpdateDeleteReposV1


class CommentListCreateServiceInterface(Protocol):
    def get_comments(self, post_id: int): ...

    def create_comment(self, post_id: int, data: OrderedDict): ...


class CommentGetUpdateDeleteServiceInterface(Protocol):
    def get_comment(self, pk: int): ...

    def like_comment(self, pk: int, user): ...


class CommentListCreateServiceV1:
    comment_repos: CommentListCreateReposInterface = CommentListCreateReposV1()

    def get_comments(self, post_id: int):
        return self.comment_repos.get_comments(post_id=post_id)

    def create_comment(self, post_id: int, data: OrderedDict):
        return self.comment_repos.create_comment(post_id=post_id, data=data)


class CommentGetUpdateDeleteServiceV1:
    comment_repos: CommentGetUpdateDeleteReposInterface = CommentGetUpdateDeleteReposV1()

    def get_comment(self, pk: int):
        return self.get_comment(pk=pk)

    def like_comment(self, pk: int, user):
        return self.comment_repos.like_comment(pk=pk, user=user)
