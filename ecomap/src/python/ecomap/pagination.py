# coding=utf-8
from math import ceil
from flask import redirect
import functools
from flask import url_for, request, abort


class Pagination(object):
    """Internal helper class returned by :meth:`BaseQuery.paginate`.  You
    can also construct it from any other SQLAlchemy query object if you are
    working with other libraries.  Additionally it is possible to pass `None`
    as query object in which case the :meth:`prev` and :meth:`next` will
    no longer work.
    """

    def __init__(self, page, per_page, total, items):
        #: the unlimited query object that was used to create this
        #: pagination object.
        # self.query = query
        #: the current page number (1 indexed)
        self.page = page
        #: the number of items to be displayed on a page.
        self.per_page = per_page
        #: the total number of items matching the query
        self.total = total
        #: the items for the current page
        self.items = items

    @property
    def pages(self):
        """The total number of pages"""
        if self.per_page == 0:
            pages = 0
        else:
            pages = int(ceil(self.total / float(self.per_page)))
        return pages

    # def prev(self, error_out=False):
    #     """Returns a :class:`Pagination` object for the previous page."""
    #     assert self.query is not None, 'a query object is required ' \
    #                                    'for this method to work'
    #     return self.query.paginate(self.page - 1, self.per_page, error_out)

    @property
    def prev_num(self):
        """Number of the previous page."""
        return self.page - 1

    @property
    def has_prev(self):
        """True if a previous page exists"""
        return self.page > 1

    # def next(self, error_out=False):
    #     """Returns a :class:`Pagination` object for the next page."""
    #     assert self.query is not None, 'a query object is required ' \
    #                                    'for this method to work'
    #     return self.query.paginate(self.page + 1, self.per_page, error_out)

    @property
    def has_next(self):
        """True if a next page exists."""
        return self.page < self.pages

    @property
    def next_num(self):
        """Number of the next page"""
        return self.page + 1

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        """Iterates over the page numbers in the pagination.  The four
        parameters control the thresholds how many numbers should be produced
        from the sides.  Skipped page numbers are represented as `None`.
        This is how you could render such a pagination in the templates:

        .. sourcecode:: html+jinja

            {% macro render_pagination(pagination, endpoint) %}
              <div class=pagination>
              {%- for page in pagination.iter_pages() %}
                {% if page %}
                  {% if page != pagination.page %}
                    <a href="{{ url_for(endpoint, page=page) }}">{{ page }}</a>
                  {% else %}
                    <strong>{{ page }}</strong>
                  {% endif %}
                {% else %}
                  <span class=ellipsis>…</span>
                {% endif %}
              {%- endfor %}
              </div>
            {% endmacro %}
        """
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1
                and num < self.page + right_current) \
                    or num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num


def paginate(query, page, per_page=20, error_out=True):
        """Returns `per_page` items from page `page`.  By default it will
        abort with 404 if no items were found and the page was larger than
        1.  This behavor can be disabled by setting `error_out` to `False`.

        Returns an :class:`Pagination` object.
        """
        if error_out and page < 1:
            abort(404)
        items = self.limit(per_page).offset((page - 1) * per_page).all()
        if not items and page != 1 and error_out:
            abort(404)

        # No need to count if we're on the first page and there are fewer
        # items than we expected.
        if page == 1 and len(items) < per_page:
            total = len(items)
        else:
            total = self.order_by(None).count()

        return Pagination(self, page, per_page, total, items)


def paginate_deco(collection, max_per_page=25):
    """Generate a paginated response for a resource collection.

    Routes that use this decorator must return a SQLAlchemy query as a
    response.

    The output of this decorator is a Python dictionary with the paginated
    results. The application must ensure that this result is converted to a
    response object, either by chaining another decorator or by using a
    custom response object that accepts dictionaries."""
    def decorator(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            # invoke the wrapped function
            query = f(*args, **kwargs)

            # obtain pagination arguments from the URL's query string
            page = request.args.get('page', 1, type=int)
            per_page = min(request.args.get('per_page', max_per_page,
                                            type=int), max_per_page)
            expanded = None
            if request.args.get('expanded', 0, type=int) != 0:
                expanded = 1

            # run the query with Flask-SQLAlchemy's pagination
            p = query.paginate(page, per_page)

            # build the pagination metadata to include in the response
            pages = {'page': page, 'per_page': per_page,
                     'total': p.total, 'pages': p.pages}
            if p.has_prev:
                pages['prev_url'] = url_for(request.endpoint, page=p.prev_num,
                                            per_page=per_page,
                                            expanded=expanded, _external=True,
                                            **kwargs)
            else:
                pages['prev_url'] = None
            if p.has_next:
                pages['next_url'] = url_for(request.endpoint, page=p.next_num,
                                            per_page=per_page,
                                            expanded=expanded, _external=True,
                                            **kwargs)
            else:
                pages['next_url'] = None
            pages['first_url'] = url_for(request.endpoint, page=1,
                                         per_page=per_page, expanded=expanded,
                                         _external=True, **kwargs)
            pages['last_url'] = url_for(request.endpoint, page=p.pages,
                                        per_page=per_page, expanded=expanded,
                                        _external=True, **kwargs)

            # generate the paginated collection as a dictionary
            if expanded:
                results = [item.export_data() for item in p.items]
            else:
                results = [item.get_url() for item in p.items]

            # return a dictionary as a response
            return {collection: results, 'pages': pages}
        return wrapped
    return decorator
