---
title: How to unit test Django's Function Based Views
description: 
date: 2014-07-31T13:27:58
slug: how-to-unit-test-djangos-function-based-views
draft: false
categories:
  - wordpress
  - testing
  - programming
tags:
  - python
---

Let's assume than the URL pattern to your Function Based View is defined like that:

`_urls.py_` 
```python
urlpatterns = patterns(
    ..., 
    url(r'^$', views.index, name='index'), 
    ...
) 
```

and your function based view looks like this: 
`_views.py_`
```python
@api_view(['GET']) @permission_classes((AllowAny,))
def index(request): 
    data = { 'field': 'value' } 
    return Response(data) 
```

Then you can unit test such view by creating a minimal instance of the `HttpRequest` 
and pass it to that view. I tried to mock to test such view with the [Mock](https://docs.python.org/3/library/unittest.mock.html) library, 
by with no luck!!! If case you know how to do it with Mock, then let me know! 

```python
def test_index_function_based_view(): 
    _request = HttpRequest() 
    _request.method = 'GET' 
    request = Request(_request) 
    response = index(request) 
    assert response.data['field'] == 'value' 
```
