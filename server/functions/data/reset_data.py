import pickle
import sys
sys.path.append("server/functions")
from helper_functions import *
reset_data()

pickle.dump(all_channels_details, open('server/functions/data/all_channels_details.p', 'wb'))
pickle.dump(all_channels_messages, open('server/functions/data/all_channels_messages.p', 'wb'))
pickle.dump(all_channels_permissions, open('server/functions/data/all_channels_permissions.p', 'wb'))
pickle.dump(list_of_users, open('server/functions/data/list_of_users.p', 'wb'))
pickle.dump(number_of_channels, open('server/functions/data/number_of_channels.p', 'wb'))
pickle.dump(number_of_messages, open('server/functions/data/number_of_messages.p', 'wb'))
pickle.dump(number_of_users, open('server/functions/data/number_of_users.p', 'wb'))
