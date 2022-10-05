from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    note = ('Тип тренировки: {training_type};'
            ' Длительность: {duration:.3f} ч.;'
            ' Дистанция: {distance:.3f} км;'
            ' Ср. скорость: {speed:.3f} км/ч;'
            ' Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:

        return self.note.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    M_IN_KM = 1000
    LEN_STEP = 0.65
    MIN_PER_H = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:

        self.action = action
        self.duration = duration
        self.duration_min = duration * self.MIN_PER_H
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
        numerator = (num - coeff_c2) * self.weight

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


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    tr: dict[str, list[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking}

    if tr.get(workout_type):

        creation = tr[workout_type](*data)
        return creation

    else:

        raise Exception('Поддерживаются только коды "SWM", "RUN", "WLK"')


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
