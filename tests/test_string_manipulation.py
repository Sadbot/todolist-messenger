import todolist.utils.string_manipulation as sm


async def test_snake_case():
    test_data = {
        'test': 'test',
        'PascalCase': 'pascal_case',
        'camelCase': 'camel_case',
        'camelWITHUpper': 'camel_with_upper',
        'camel1WithNumber': 'camel1_with_number',
        'camel1WITHUpper': 'camel1_with_upper',
    }
    for input, expected in test_data.items():
        result = sm.to_snake_case(input)
        assert result == expected
