import datetime
import numpy as np
from collections import namedtuple

Message = namedtuple('message', 'uid risk day unobs_id')
UpdateMessage = namedtuple('update_message', 'uid new_risk risk day received_at unobs_id')

def encode_message(message):
	# encode a contact message as a string
	return str(message.uid) + "_" + str(message.risk) + "_" + str(message.day)  + "_" + str(message.unobs_id)

def encode_update_message(message):
	# encode a contact message as a string
	return str(message.uid) + "_" + str(message.new_risk) + "_" + str(message.risk) + "_" + str(message.day) + "_" + str(message.received_at) + "_" + str(message.unobs_id)

def decode_message(message):
	# decode a string-encoded message into a tuple
	uid, risk, day, unobs_id = message.split("_")
	obs_uid = int(uid)
	risk = int(risk)
	day = int(day)
	unobs_uid = unobs_id
	return Message(obs_uid, risk, day, unobs_uid)

def decode_update_message(update_message):
	# decode a string-encoded message into a tuple
	uid, new_risk, risk, day, received_at, unobs_id = update_message.split("_")
	obs_uid = int(uid)
	risk = int(risk)
	new_risk = int(new_risk)
	day = int(day)
	received_at = datetime.datetime.strptime(received_at, "%Y-%m-%d %H:%M:%S")
	unobs_uid = unobs_id
	return UpdateMessage(obs_uid, new_risk, risk, day, received_at, unobs_uid)

def create_new_uid(rng):
	# generate a 4 bit random code
	return np.random.randint(0, 15)

def update_uid(_uid, rng):
	_uid = "{0:b}".format(_uid).zfill(4)[1:]
	_uid += rng.choice(['1', '0'])
	return int(_uid, 2)

def compare_uids(uid1, uid2, days_apart):
	bin_uid1 = "{0:b}".format(uid1).zfill(4)
	bin_uid2 = "{0:b}".format(uid2).zfill(4)
	if days_apart == 1 and bin_uid1[:3] == bin_uid2[1:]:
		return True
	if days_apart == 2 and bin_uid1[:2] == bin_uid2[2:]:
		return True
	if days_apart == 3 and bin_uid1[:1] == bin_uid2[3:]:
		return True
	return False

def hash_to_cluster(message):
	bin_uid = "{0:b}".format(message.uid).zfill(4)
	bin_risk = "{0:b}".format(message.risk).zfill(4)
	# bin_day = "{0:b}".format(message.day).zfill(24)
	binary = "".join([bin_uid, bin_risk])
	cluster_id = int(binary, 2)
	# print(f"cluster: {cluster_id}, bin: {binary}")
	return cluster_id
