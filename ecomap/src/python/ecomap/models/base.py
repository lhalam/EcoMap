'''Base view class.'''


class BaseModel(object):

    """Base class for working with models."""

    def get_all(self):
        '''Method to retrieves data.'''
        pass

    def save(self):
        '''Method to add data.'''
        pass

    def edit(self):
        '''Method to edit data.'''
        pass

    def delete(self):
        '''Method to delete data.'''
        pass
