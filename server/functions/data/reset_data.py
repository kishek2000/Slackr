import pickle
from ../helper_functions import *
reset_data()

pickle.dump(all_channels_details, open('all_channels_details.p', 'wb'))
pickle.dump(all_channels_messages, open('all_channels_messages.p', 'wb'))
pickle.dump(all_channels_permissions, open('all_channels_permissions.p', 'wb'))
pickle.dump(list_of_users, open('list_of_users.p', 'wb'))
pickle.dump(number_of_channels, open('number_of_channels.p', 'wb'))
pickle.dump(number_of_messages, open('number_of_messages.p', 'wb'))
