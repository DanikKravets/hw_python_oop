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

        m1 = f'Тип тренировки: {self.training_type};'
        m2 = f' Длительность: {self.duration} ч.;'
        m3 = f' Дистанция: {self.distance} км;'
        m4 = f' Ср. скорость: {self.speed} км/ч;'
        m5 = f' Потрачено ккал: {self.calories}.'
        message = m1 + m2 + m3 + m4 + m5

        return message


class Training:
    """Базовый класс тренировки."""

    M_IN_KM = 1000
    LEN_STEP = 0.65
    NAME = 'Training'  # В каждом классе будет разное значение этой переменной

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:

        self.action = action
        self.duration = duration
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

        information = InfoMessage(self.NAME,
                                  self.duration,
                                  self.get_distance(),
                                  self.get_mean_speed(),
                                  self.get_spent_calories())
        return information


class Running(Training):
    """Тренировка: бег."""

    NAME = 'Running'

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для класса Running."""

        coeff_c1 = 18  # Коэффициенты калорий
        coeff_c2 = 20
        duration_min = self.duration * 60  # Перевод часов в минуты
        num = coeff_c1 * self.get_mean_speed()
        numerator = (num - coeff_c2) * self.weight  # Соблюдение 79 символов

        return numerator / self.M_IN_KM * duration_min


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    NAME = 'SportsWalking'

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
        duration_min = self.duration * 60  # Перевод часов в минуты
        dg = (self.get_mean_speed() ** 2 // self.weight)
        sum = coeff_1 * self.weight + dg * coeff_2 * self.weight

        return sum * duration_min


class Swimming(Training):
    """Тренировка: плавание."""

    NAME = 'Swimming'
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


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    tr = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    if len(data) == 5:
        cr = tr[workout_type](data[0], data[1], data[2], data[3], data[4])

    elif len(data) == 3:
        cr = tr[workout_type](data[0], data[1], data[2])

    else:
        cr = tr[workout_type](data[0], data[1], data[2], data[3])

    return cr


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
