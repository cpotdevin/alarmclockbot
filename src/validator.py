STEP_TYPES = [
    'AUDIO_FILE',
    'SIMPLE_TEXT',
    'TIMESTAMP_TEXT'
]

def validateStep(step):
    if step.get('type') is None:
        raise AttributeError('Steps must include a "type" attribute.')
    elif step.get('type') not in STEP_TYPES:
        raise AttributeError(f'Steps must use a valid step type: {STEP_TYPES}')
    elif step.get('type').endswith('TEXT') and step.get('text') is None:
        raise AttributeError('TEXT type steps must include a "text" attribute')
    elif step.get('type').endswith('FILE') and step.get('file') is None:
        raise AttributeError('FILE type steps must include a "file" attribute')
