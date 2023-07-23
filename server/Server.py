import json
from xmlrpc.server import SimpleXMLRPCRequestHandler
from xmlrpc.server import SimpleXMLRPCServer

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from repo.FileRepo import FileRepo
from service.FileService import FileService


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/XMLRPC',)


if __name__ == "__main__":
    server = SimpleXMLRPCServer(('localhost', 8080), requestHandler=RequestHandler)
    server.register_introspection_functions()
    connection_string = 'mysql://root:root@localhost/fisiere'
    engine = create_engine(connection_string)
    Session = sessionmaker(bind=engine)
    conn = engine.connect()
    session = Session(bind=conn)

    file_repo = FileRepo(session)
    service = FileService(file_repo)


    def find_all_files():
        files = service.find_all_files()
        files_json = json.dumps(files, default=lambda x: x.to_dict())
        return files_json


    server.register_function(find_all_files, 'find_all_files')


    def find_files_containing_substring(substring):
        files = service.find_files_containing_substring(substring)
        files_json = json.dumps(files, default=lambda x: x.to_dict())
        return files_json


    server.register_function(find_files_containing_substring, 'find_files_containing_substring')


    def find_files_by_content_parts_text(content):
        files = service.find_files_by_content_parts_text(content)
        files_json = json.dumps(files, default=lambda x: x.to_dict())
        return files_json


    server.register_function(find_files_by_content_parts_text, 'find_files_by_content_parts_text')


    def find_files_by_content_parts_binary(content):
        files = service.find_files_by_content_parts_binary(content)
        files_json = json.dumps(files, default=lambda x: x.to_dict())
        return files_json


    server.register_function(find_files_by_content_parts_binary, 'find_files_by_content_parts_binary')


    def find_files_with_duplicate_hash():
        files = service.find_files_with_duplicate_hash()
        files_json = json.dumps(files, default=lambda x: x.to_dict())
        return files_json


    server.register_function(find_files_with_duplicate_hash, 'find_files_with_duplicate_hash')

    server.serve_forever()
