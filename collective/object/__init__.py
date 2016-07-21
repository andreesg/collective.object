from zope.i18nmessageid import MessageFactory as BaseMessageFactory

# Set up the i18n message factory for our package
MessageFactory = BaseMessageFactory('collective.object')

def initialize(context):
    pass
