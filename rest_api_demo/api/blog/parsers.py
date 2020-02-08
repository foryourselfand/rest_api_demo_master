from flask_restplus import reqparse

pagination_arguments = reqparse.RequestParser()
pagination_arguments.add_argument('page', type = int, required = False, default = 1, help = 'Page number')
pagination_arguments.add_argument('per_page', type = int, required = False, choices = [2, 10, 20, 30, 40, 50],
                                  default = 10, help = 'Results per page')

comparison_arguments = reqparse.RequestParser()
comparison_arguments.add_argument('city_first', type = str, required = True, default = 'Санкт-Петербург',
                                  help = 'Name of the first city (in Russian)')
comparison_arguments.add_argument('city_second', type = str, required = True, default = 'Владивосток',
                                  help = 'Name of the second city (in Russian)')
