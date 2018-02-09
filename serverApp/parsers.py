from serverApp.models import Schedule


class ScheduleParser:

    def parse(self, json):

        # JSON Layer

        # Разбиваем все занятия на две недели (числитель и знаменатель).
        json = self.divide(json=json)

        # Удаляем ненужные символы.
        json = self.remove_symbols(json=json)

        # Models Layer

        # Пока не готова БД уровня с моделями не будет.
        # Поэтому на этом уровне мы будем видоизменять JSON в нужный вид.
        # Подробности тут - github.com/BMSTUScheduleTeam/BMSTUScheduleServer/issues/9

        json = self.transform_json(json=json)

        return json

    def divide(self, json):

        json_list = list(json)
        if len(json_list) == 0:
            return {"nominator": None, "denominator": None}

        days = json[0]['studyWeek']

        # Разбиваем все занятия на две недели (числитель и знаменатель).

        nominator_days = []
        denominator_days = []

        for day in days:

            periods = day["periods"]
            nominator_periods = []
            denominator_periods = []

            for period in periods:

                study_classes = period["studyClasses"]
                nominator_classes = []
                denominator_classes = []

                for study_class in study_classes:

                    study_class_type = study_class["type"]

                    if study_class_type == "nominator":
                        nominator_classes.append(study_class)

                    elif study_class_type == "denominator":
                        denominator_classes.append(study_class)

                    else:
                        nominator_classes.append(study_class)
                        denominator_classes.append(study_class)

                nominator_period = dict(period)
                nominator_period["studyClasses"] = nominator_classes
                nominator_periods.append(nominator_period)

                denominator_period = dict(period)
                denominator_period["studyClasses"] = denominator_classes
                denominator_periods.append(denominator_period)

            nominator_day = dict(day)
            nominator_day["periods"] = nominator_periods
            nominator_days.append(nominator_day)

            denominator_day = dict(day)
            denominator_day["periods"] = denominator_periods
            denominator_days.append(denominator_day)

        return {"nominator": nominator_days, "denominator": denominator_days}

    def remove_symbols(self, json):

        # Удаляем ненужные символы из json'а.

        # Если словарь
        if isinstance(json, dict):

            for key, item in json.items():
                if isinstance(item, str):
                    json[key] = self.remove_symbols_from_item(string=item)
                elif isinstance(item, dict):
                    json[key] = self.remove_symbols(json=item)
                elif isinstance(item, list):
                    json[key] = self.remove_symbols(json=item)
                else:
                    continue

        # Если список
        elif isinstance(json, list):

            for index, item in enumerate(json):
                if isinstance(item, str):
                    json[index] = self.remove_symbols_from_item(string=item)
                elif isinstance(item, dict):
                    json[index] = self.remove_symbols(json=item)
                elif isinstance(item, list):
                    json[index] = self.remove_symbols(json=item)
                else:
                    continue

        return json

    def remove_symbols_from_item(self, string):

        # Удаляем ненужные символы из строки.

        # Удаляем "null"
        string = string.replace("null", "")

        # Удаляем "\xa0"
        string = string.replace("\xa0", " ")

        # Удаляем больше одного пробела.
        string = string.replace("  ", " ")
        string = string.replace("   ", " ")

        # Удаляем пробелы на концах строки.
        if string[0] == " ":
            string = string[1:]
        if string[-1] == " ":
            string = string[:-1]

        # Первые буквы слов делаем заглавными.
        string = string.title()

        return string

    def create_model(self, json):

        # Создаем модель расписания из json'а.

        schedule = Schedule()

        # Заполняем модель

        return schedule

    def transform_json(self, json):

        # Видоизменяем json..

        return json