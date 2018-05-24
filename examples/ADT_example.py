from collections import defaultdict

class DataStorage:
	
	def __init__(self):
		self.accounts_list = []
		self.files_tree = defaultdict()

	def capacity(self):
		"""Return the compound cloud storages capacity left."""		
		print("To be implemented")
		return None


	def search(self, query_name):
		"""Returns info(cloud storage account, path, size, link to download, option to delete) about the files
		or directory if it exists in the storage, otherwise returns message notifying that there is no item found."""
		print("To be implemented")
		return None

	def upload(self, id):
		"""Return True if the upload of the file or folder was successful, otherwise False"""
		print("To be implemented")
		return None

	def sync(self, id):
		"""Return True if the synchronization option was successfully activated, otherwise False"""
		print("To be implemented")
		return None
	

	def deactivate_sync(self, id):
		"""Return True if the synchronization option was sucessfully deactivated, otherwise False"""
		print("To be implemented")
		return None
	

	def delete_file(self, id):
		"""Return True if the deletion was successfully executed, otherwise False"""
		print("To be implemented")
		return None


	def link_account(self, id):
		"""Return True if the the cloud storage account was successfully added to the already linked ones, otherwise False"""
		print("To be implemented")
		return None


	def unlink_account(self, id):
		"""Return True if the the cloud storage account was successfully removed from the list of linked ones, otherwise False"""
		print("To be implemented")
		return None


	def download_file(self, id):
		"""Return True if the contents of the path was successfully downloaded to the downloads folder, otherwise False"""
		print("To be implemented")
		return None

if __name__ == "__main__":
	obj = DataManager()
	obj.search("a.exe")
	obj.upload("a.exe")
	obj.sync("a.exe")
	obj.deactivate_sync("a.exe")
	obj.delete_file("a.exe")
	obj.link_account("a.exe")
	obj.unlink_account("a.exe")
	obj.download_file("a.exe")