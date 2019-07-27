STEP_TYPES = [
    'AUDIO_FILE',
    'SIMPLE_TEXT',
    'TIMESTAMP_TEXT',
    'API_TEXT'
]

def validateStep(step):
    if step.get('type') is None:
        raise AttributeError('Steps must include a "type" attribute.')
    elif step.get('type') not in STEP_TYPES:
        raise AttributeError(f'Steps must use a valid step type: {STEP_TYPES}')
    elif step.get('type').endswith('TEXT'):
        if step.get('text') is None:
            raise AttributeError('TEXT type steps must include a "text" attribute')
        elif step.get('type') == 'API_TEXT':
            if step.get('url') is None:
                raise AttributeError('API_TEXT type steps must include a "url" attribute')
            elif step.get('paths') is None:
                raise AttributeError('API_TEXT type steps must include a "paths" attribute')

    elif step.get('type').endswith('FILE') and step.get('file') is None:
        raise AttributeError('FILE type steps must include a "file" attribute')
