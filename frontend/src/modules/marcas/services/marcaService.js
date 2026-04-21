const URL = 'http://localhost:8000/api/marcas/';

export const getMarcas = async () => {
    const response = await fetch(URL, {
        credentials: 'include'
    });
    return response.json()
}

export const createMarca = async (data) => {
    const  response = await fetch(URL, 
        {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    return response.json()
}

export const updateMarca = async (id, data) => {
    const response = await fetch(`${URL}${id}/`, 
        {
            method: 'PUT',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
    return response.json()
}

export const deleteMarca = async (id) => {
    await fetch(`${URL}${id}/`,
        {
            method: 'DELETE',
            credentials: 'include'
        })
}
