from DBObject.Row import Row


class JointsGenerator:

    def __init__(self, total_size: int, good_data: int):
        self.total_size = total_size
        self.good_data = good_data
        self.waste_data = self.total_size - good_data

    # this function guarantuee selectivity
    # in fact it is equal condition but based on row_id, not value
    # what is simpler than data generation
    # n-n relation
    def condition(self, left_row: Row, right_row: Row)->bool:
        lid = left_row.GetId()
        rid = right_row.GetId()

        return lid < self.good_data and rid < self.good_data
