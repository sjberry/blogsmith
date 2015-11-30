from dropbox.client import DropboxClient as BaseClient


class DropboxClient(BaseClient):
    def get_files(self, path, recursive=False):
        metadata = self.metadata(path)

        for entity in metadata['contents']:
            if not entity['is_dir']:
                yield entity['path'], entity['rev']
