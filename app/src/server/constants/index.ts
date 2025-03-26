// TODO:
// - if this works, move to constants and/or devise way to get this based on env
// - figure out why the container isn't recognizing requests to 'https://nlp-ssa.dev'
// ---- NOTE: maybe it's something about networking that I don't know shit about? :]
export const baseRequestURL = process.env.ENV !== 'production' ? 'http://server:3000' : 'https://nlp-ssa.dev';
