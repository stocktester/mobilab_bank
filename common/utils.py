from rest_framework.generics import ListCreateAPIView
from rest_framework import status
from rest_framework.response import Response


class UrlLisCreateAPIView(ListCreateAPIView):

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ReverseDict(dict):

    def __setitem__(self, key, value):

        if key in self:
            del self[key]
        if value in self:
            del self[value]

        dict.__setitem__(self, key, value)
        dict.__setitem__(self, value, key)

    def __delitem__(self, key):

        dict.__delitem__(self, self[key])
        dict.__delitem__(self, key)

    def __len__(self):

        return dict.__len__(self) // 2


class ChoiceDict(ReverseDict):

    def __init__(self, choice_tuple: tuple = None):

        holder_dict = {x[0]: x[1] for x in choice_tuple}
        super().__init__(**holder_dict)


