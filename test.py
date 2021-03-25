import handler

def test_get_ec2_recovery_stats():
	response = handler.get_ec2_recovery_stats()

	print(response)

if __name__ == '__main__':
    test_get_ec2_recovery_stats()