if __name__ == "__main__":

    from mongoengine import *
    import tk_rest
    connect(
        'diary'
    )

    class note_diary(Document):
        note_summary = StringField()
        author_id = StringField()
        time = StringField()
        classroom_id = StringField()
        _id = StringField

        def json(self):
            return {
                "id": self.id,
                "author_id": self.author_id,
                "classroom_id": self.classroom_id,
                "note_summary": self.note_summary,    
            }


    class note_noteprecise(Document):
        _id = StringField()
        for_student = StringField()
        diary_id = StringField()
        note = StringField()

        def json(self):
            return {
                "id": self.id,
                "diary_id": self.diary_id,
                "member_id": self.for_student,
                "note": self.note 
            }


    # for class diary
    list_data_class = [note_diary.json() for note_diary in note_diary.objects ] 
    data_class = list_data_class

    # for student diary
    list_data = [note.json() for note in note_noteprecise.objects]

    data_note = list_data

    data = [data_class, data_note]


    t = tk_rest.TKRest("http://dev-diary.herokuapp.com/api")

    t.dumpdata.post(data)
    print("saved")

