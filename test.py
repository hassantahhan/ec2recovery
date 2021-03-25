import handler

def test_get_ec2_recovery_stats():
	print('### Test 1: handler.get_ec2_recovery_stats...')
	print(handler.get_ec2_recovery_stats())
	print('### Test 2: handler.refresh_ec2_recovery_stats...')
	print(handler.refresh_ec2_recovery_stats('2021-03-25T14:44:22.135643'))
	print('### Test End!')

if __name__ == '__main__':
    test_get_ec2_recovery_stats()