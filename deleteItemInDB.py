import couchdb

server = couchdb.Server()
db = server['tweets-example']

for item in db:
	if db[item]['coordinates'] == None:
		print item
		db.delete(db[item])
		# print db[item]['coordinates']['coordinates']