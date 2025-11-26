function a() {
    const l = [];
    let i;
    for (i = 0; i < 4; i++) {
        l.push(() => (i));
    }
    return l;
}

a().map((f) => (console.log(f())))

// Oh no... I have serious misunderstanding of closures...
