import os


class ProjectHelper:
    @staticmethod
    def get_project_name(full_url):
        result = ''

        name_splitted = str.split(full_url, '/')
        if len(name_splitted) > 2:
            # https://www.eclipse.org/paho/
            last_name = name_splitted.pop()
            while last_name == '':
                last_name = name_splitted.pop()
            result = last_name.lower()
        else:
            result = full_url.lower()

        # remove the 'iot'
        result = result.replace('iot', '').replace('.', ' ').strip()

        # remove the 'technology'
        result = result.replace('technology', '').replace('.', ' ').strip()

        # remove the 'tools'
        result = result.replace('tools', '').replace('.', ' ').strip()

        # handle special case
        if('agile' in result):
            result = 'agile'

        return result

    @staticmethod
    def create_data_folder(folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    @staticmethod
    def load_raw_data_file(project_name):
        data_path = './data/scrapy/'
        default_encoding = 'utf-8'
        with open(data_path + project_name + '.txt', 'r', encoding=default_encoding) as dataFile:
            return dataFile.readlines()
