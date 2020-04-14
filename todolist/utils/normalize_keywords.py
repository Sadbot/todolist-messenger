from todolist.models import Command, CommandNkeywords
from todolist.utils.morph_analyzer import MorphAnalyzer


def normalize_keywords(db_session_manager):
    morph = MorphAnalyzer()

    session = db_session_manager()
    commands = session.query(Command).all()
    objects = []
    for command in commands:
        for i in range(1, 6):
            keys = getattr(command, f"keywords{i}")
            if keys:
                norm_keys = morph.analyze_normal_sentences(keys)
                for keyword in norm_keys:
                    objects.append(CommandNkeywords(keyword=keyword, group=i, command_id=command.id))

    session.bulk_save_objects(objects)
    session.commit()
