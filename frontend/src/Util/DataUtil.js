export function getDefaultData(fields) {
    let data = []
    for (let i = 0; i < fields.length; i++) {
        data.push(getDefaultValue(fields[i].type))
    }
    return data
}

function getDefaultValue(type) {
    if (type === 'string') {
        return ''
    } else if (type === 'boolean') {
        return false
    } else if (type === 'pid') {
        return {p: '', i: '', d: ''}
    }
    return null
}