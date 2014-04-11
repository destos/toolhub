def models_to_query(*models):
    '''takes a list of models and converts it into a compareable list'''
    return map(repr, list(models))
