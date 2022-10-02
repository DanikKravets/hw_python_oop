def rounder(num, digits=0):
    """Оставляет столько знаков, после запятой, сколько нужно в любом случае"""

    return f'{num:.{digits}f}'


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:

        self.training_type = training_type
        self.duration = rounder(duration, 3)
        self.distance = rounder(distance, 3)
        self.speed = rounder(speed, 3)
        self.calories = rounder(calories, 3)

    def get_message(self) -> str:

        message = ''.join((f'Тип тренировки: {self.training_type};',
                           f' Длительность: {self.duration} ч.;'
                           f' Дистанция: {self.distance} км;',
                           f' Ср. скорость: {self.speed} км/ч;',
                           f' Потрачено ккал: {self.calories}.'))
        return message


class Training:
    """Базовый класс тренировки."""

    M_IN_KM = 1000
    LEN_STEP = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:

        min_per_h = 60
        self.action = action
        self.duration = duration
        self.duration_min = duration * min_per_h
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        return (self.action * self.LEN_STEP) / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        information = InfoMessage(self.__class__.__name__,
                                  self.duration,
                                  self.get_distance(),
                                  self.get_mean_speed(),
                                  self.get_spent_calories())
        return information


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для класса Running."""

        coeff_c1 = 18  # Коэффициенты калорий
        coeff_c2 = 20
        num = coeff_c1 * self.get_mean_speed()
        numerator = (num - coeff_c2) * self.weight  # Соблюдение 79 символов

        return numerator / self.M_IN_KM * self.duration_min


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:

        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для класса SportWalking."""

        coeff_1 = 0.035
        coeff_2 = 0.029
        dg = (self.get_mean_speed() ** 2 // self.weight)
        sum = coeff_1 * self.weight + dg * coeff_2 * self.weight

        return sum * self.duration_min


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: float
                 ) -> None:

        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения в классе Swimming."""

        mul = self.length_pool * self.count_pool / self.M_IN_KM
        return mul / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для класса Swimming."""

        coeff_3 = 1.1
        coeff_4 = 2
        sum = self.get_mean_speed() + coeff_3
        return sum * coeff_4 * self.weight


def invalid_code(data: list) -> Exception:

    raise Exception('Поддерживаются только коды "SWM", "RUN", "WLK" ')


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    tr: dict[str, list[int]] = {
        'SWM': lambda data: Swimming(*data),
        'RUN': lambda data: Running(*data),
        'WLK': lambda data: SportsWalking(*data)}

    creation = tr.get(workout_type, invalid_code)
    return creation(data)


def main(training: Training) -> None:
    """Главная функция."""

    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
