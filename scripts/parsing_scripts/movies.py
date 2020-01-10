from typing import List

names = ["phantom_menace", "attack_of_the_clones", "revenge_of_the_sith"]

name_dict = {
    "phantom_menace": 0,
    "attack_of_the_clones": 1,
    "revenge_of_the_sith": 2
}


class NotAPrequel(Exception):
    def __init__(self, movie: str):
        super().__init__(f'"{movie}" is not a proper Prequel movie format')


class Movie:
    PHANTOM_MENACE = 0
    ATTACK_OF_THE_CLONES = 1
    REVENGE_OF_THE_SITH = 2

    def __init__(self, name: str):
        if name not in names:
            raise NotAPrequel
        self.name = name


class Movies:
    def __init__(self, names: List[str]):
        self.movies = []
        for name in names:
            if name not in names:
                raise NotAPrequel
            self.movies.append(Movie(name))

    def __contains__(self, item: str):
        return item in names


movies = Movies(names)

