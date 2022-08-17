import pusher
import sys, os
sys.path.append(os.path.abspath('../'))
import secret

pusher_client = pusher.Pusher(
app_id = secret.PUSHER_APP_ID,
key = secret.PUSHER_KEY,
secret = secret.PUSHER_SECRET,
cluster = secret.PUSHER_CLUSTER,
ssl=True
)

