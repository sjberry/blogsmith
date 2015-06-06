from dropbox.client import DropboxClient as BaseClient


class DropboxClient(BaseClient):
    def get_file_names(self, path, recursive=False):
        metadata = self.metadata(path)
        files = []

        for entity in metadata['contents']:
            if not entity['is_dir']:
                files.append(entity['path'])

        return files
