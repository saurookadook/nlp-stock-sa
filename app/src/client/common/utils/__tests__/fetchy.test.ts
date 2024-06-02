import { AmbiguousObject } from '@nlpssa-app-types/common/main';
import fetchy from 'client/common/utils/fetchy';

const baseCatApiURL = 'http://cat-names.io';
const catNameData = [
    { id: '07c134fd-c342-49e8-91a7-6257730af4e6', name: 'Buddy' },
    { id: 'd1842724-ec6a-42f9-bb38-081799f2d396', name: 'Zero' },
    { id: '77b59441-3307-4a45-a892-20da1b5d571e', name: 'Gordo' },
    { id: 'eb391ded-c477-4b34-b016-c70b8abc0ebe', name: 'Sherman' },
    { id: '9b01a4ab-6461-4b62-8519-aaaf5e4c5ed9', name: 'Grandma' },
    { id: 'bc1d0540-ccc7-4878-b843-c90d37facfde', name: 'Bailey' },
    { id: 'bfffc494-e4bb-4f6a-bd2e-53a5a24c4942', name: 'Spot' },
    { id: '3c679338-c262-45ba-bc0d-208229744931', name: 'Lucifer' },
    { id: '6fb0b79d-60a6-45a3-b565-b4da286bc422', name: 'Mr. Twinkletoes' },
];

function MockResponsePromise(bodyJson: AmbiguousObject | null, options): Promise<Response> {
    return new Promise(function (resolve) {
        resolve(new Response(JSON.stringify(bodyJson), options));
    });
}

jest.spyOn(fetchy, '_fetch').mockImplementation((url, opts = {}) => {
    const { method } = opts;

    if (method === 'GET') {
        switch (url) {
            case `${baseCatApiURL}/all`:
            case 'http://localhost/all':
                return MockResponsePromise(
                    {
                        catNames: catNameData,
                    },
                    opts,
                );
            case `${baseCatApiURL}/aepoahwepgha`:
                return MockResponsePromise(null, {
                    ...opts,
                    status: 500,
                });
        }
    } else if (method === 'POST') {
        switch (url) {
            case `${baseCatApiURL}/names/new`:
                return MockResponsePromise(
                    {
                        reqBody: opts.body,
                        success: true,
                    },
                    opts,
                );
        }
    } else if (method === 'PUT') {
        switch (url) {
            case `${baseCatApiURL}/names/update`:
                return MockResponsePromise(
                    {
                        reqBody: opts.body,
                        success: true,
                    },
                    opts,
                );
        }
    }

    return MockResponsePromise({ success: false }, opts);
});

describe("fetchy - a 'fetch' wrapper", () => {
    afterAll(() => {
        jest.restoreAllMocks();
    });

    describe('GET requests', () => {
        it('should retrieve JSON', async () => {
            const response = await fetchy
                .get(`${baseCatApiURL}/all`)
                .then((response) => response.json())
                .then((jsonResponse) => jsonResponse);
            expect(response).toStrictEqual({
                catNames: catNameData,
            });
        });

        it('should handle relative URLs', async () => {
            const request = await fetchy.get('/all');
            expect(request.status).toBe(200);

            const response = await request.json();
            expect(response).toStrictEqual({
                catNames: catNameData,
            });
        });

        it('should handle server errors', async () => {
            const request = await fetchy.get(`${baseCatApiURL}/aepoahwepgha`);
            expect(request.status).toBe(500);
        });

        it.skip('should not permanently update headers', async () => {
            expect('implement me!').toBe(false);
        });
    });

    describe('POST requests', () => {
        it('should make request and retrieve response (with csrfToken?)', async () => {
            const newCat = { id: 'c5cd4abe-110b-4f16-8083-63634f106842', name: 'Herschel' };
            const response = await fetchy
                .post(`${baseCatApiURL}/names/new`, {
                    bodyJson: newCat,
                    options: { headers: { 'csrf-token': 'super-secure-token' } },
                })
                .then((response) => response.json())
                .then((jsonResponse) => jsonResponse);
            expect(response).toStrictEqual({
                reqBody: newCat,
                success: true,
            });
        });
    });

    describe('PUT requests', () => {
        it('should make request and retrieve response (with csrfToken?)', async () => {
            const updateLuciferName = { id: '3c679338-c262-45ba-bc0d-208229744931', name: 'Fluffy' };
            const response = await fetchy
                .put(`${baseCatApiURL}/names/update`, {
                    bodyJson: updateLuciferName,
                    options: { headers: { 'csrf-token': 'super-secure-token' } },
                })
                .then((response) => response.json())
                .then((jsonResponse) => jsonResponse);
            expect(response).toStrictEqual({
                reqBody: updateLuciferName,
                success: true,
            });
        });
    });
});
