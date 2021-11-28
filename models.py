from typing import Optional


class ModelwithPrimaryKey:

    def __init__(
            self,
            key: int,
            *args,
            **kwargs
    ):
        self.id = key


class Answer(ModelwithPrimaryKey):
    def __init__(
            self,
            key: int,
            answer: str,
            score: int
    ):
        super().__init__(key=key)
        self.answer = answer
        self.score = score


class Question(ModelwithPrimaryKey):

    def __init__(
            self,
            key: int,
            title: int,
            answers: list[Answers]
    ):
        super().__init__(key=key)
        self.title = title
        self.answers = answers


class Factor(ModelwithPrimaryKey):

    def __init__(
            self,
            key: int,
            name: int,
    ):
        super().__init__(key=key)
        self.name = name


class Aspect(ModelwithPrimaryKey):

    def __init__(
            self,
            key: int,
            name: int,
            questions: list[Question],
            factors: Optional[list[Factor]]
    ):
        super().__init__(key=key)
        self.name = name
        self._questions = questions


class Threshhold(ModelwithPrimaryKey):

    def __init__(
            self,
            key: int,
            value: int,
            message: str,
            aspect: Aspect
    ):
        super().__init__(key=key)
        self.value = value
        self.aspect = aspect
        self.message = message


class Dimension(ModelwithPrimaryKey):

    def __init__(
            self,
            key: int,
            name: str,
            weight_factor: int,
            scan: Scan,
            thresholds: list[Aspect],
            aspects: list[Aspect],
            questions: Optional[list[Question]]
    ):
        super().__init__(key=key)
        self._name = name
        self._weight_factor = weight_factor
        self._scan = scan
        self._thresholds = thresholds
        self._aspects = aspects
        self._questions = questions


class Scan(ModelwithPrimaryKey):

    def __init__(
            self,
            key: int,
            company: Company,
            is_internal: bool
    ):
        super().__init__(key=key)
        self.company = company
        self.is_internal = is_internal


class Company(ModelwithPrimaryKey):

    def __init__(
            self,
            key: int,
            name: str,
    ):
        super().__init__(key=key)
        self.name = name
