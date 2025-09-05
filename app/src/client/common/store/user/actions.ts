import { ATTEMPT_LOGOUT, COMPLETE_LOGOUT } from 'client/common/constants/actionTypes';

export async function attemptLogout({ dispatch }) {
    dispatch({ type: ATTEMPT_LOGOUT });

    const logPrefix = `[common : ${attemptLogout.name}]`;

    try {
        const apiResponse = await fetch(`/api/auth/logout`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                Credentials: 'include',
            },
        });

        const apiData = await apiResponse.json();

        if (apiResponse.status >= 400 || apiData.detail) {
            const errorMessage = apiData.message || apiData.detail;
            throw new Error(errorMessage);
        }

        console.log(`${logPrefix} - apiResponse:`, { apiResponse });
        completeLogout({ dispatch });

        return apiData;
    } catch (e) {
        console.warn(`${logPrefix} - caught exception:\n`, e);
        return null;
    }
}

export async function completeLogout({ dispatch }) {
    return dispatch({ type: COMPLETE_LOGOUT });
}
