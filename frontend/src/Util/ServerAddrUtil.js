export function getURL(route, useLocalhost) {
    let ret = ''
    if (useLocalhost) {
        ret += 'http://localhost:6969'
    } else {
        ret += 'http://192.168.203.1:6969'
    }
    ret += '/'
    ret += route
    return ret
}