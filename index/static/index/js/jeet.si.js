/*meet.jit.si*/
function jeet(nome_da_empresa) {
    const domain = 'meet.jit.si';
    const options = {
        roomName: nome_da_empresa,
        parentNode: document.querySelector('#meet')
    };
    const api = new JitsiMeetExternalAPI(domain, options);
}