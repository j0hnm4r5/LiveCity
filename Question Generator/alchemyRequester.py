from alchemyapi import AlchemyAPI
from alchemyCredentials import *

import pprint

alchemy = AlchemyAPI()


text = "How much is that doggy in the window? The one being sold at Walmart. Buy from Walmart today!"

r = alchemy.entities('text', text)
pprint.pprint( r.keys() )
pprint.pprint( r['entities'] )
pprint.pprint( "**********" )

r = alchemy.keywords('text', text)
pprint.pprint( r.keys() )
pprint.pprint( r['keywords'] )
pprint.pprint( "**********" )

r = alchemy.concepts('text', text)
pprint.pprint( r.keys() )
pprint.pprint( r['concepts'] )
pprint.pprint( "**********" )

r = alchemy.sentiment('text', text)
pprint.pprint( r.keys() )
pprint.pprint( r['docSentiment'] )
pprint.pprint( "**********" )

r = alchemy.sentiment_targeted('text', text, "How")
pprint.pprint( r.keys() )
pprint.pprint( r['docSentiment'] )
pprint.pprint( "**********" )

r = alchemy.relations('text', text)
pprint.pprint( r.keys() )
pprint.pprint( r['relations'] )
pprint.pprint( "**********" )

r = alchemy.category('text', text)
pprint.pprint( r.keys() )
pprint.pprint( r['category'] )
pprint.pprint( "**********" )