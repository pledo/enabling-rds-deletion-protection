import boto3

def check_db_deletion_protection_status(db_list):
  for db in db_list:
    print("DB: {} - TerminationProtection: {}".format(\
      db['DBInstanceIdentifier'], db['DeletionProtection']))


def enable_db_deletion_protection(db_list):
  response_list = []

  for db in db_list:
    response = client.modify_db_instance(DBInstanceIdentifier=db, \
      DeletionProtection=True, ApplyImmediately=True)

    print(response["DBInstance"]['DBInstanceIdentifier'], \
      response["DBInstance"]['DeletionProtection'] )

    response_list.append(response["DBInstance"])
  return response_list

# -----------------------------------------------------

def main():

  list_of_all_dbs = client.describe_db_instances()['DBInstances']

  print("Checking the db deletion protection status, before change it\n")
  check_db_deletion_protection_status(list_of_all_dbs)

  dbs_list_to_be_changed = [ db['DBInstanceIdentifier'] for db in \
    list_of_all_dbs if db['DeletionProtection'] == False ]

  print("\nEnabling deletion protection\n")
  response = enable_db_deletion_protection(dbs_list_to_be_changed)

  print("\nChecking the changes\n")
  check_db_deletion_protection_status(response)

if __name__ == '__main__':
  client = boto3.client('rds')
  main()
