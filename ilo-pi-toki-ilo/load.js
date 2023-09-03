async function LoadStuff(){
    ctx$ = document.getElementById("canvas").getContext("2d")
    canvas$ = document.getElementById("canvas")
    ctx$.font = "12px Sitelen_Pona"
    const SitelenPona$ = new FontFace('Sitelen_Pona', 'url(ilo-pi-toki-ilo/FairfaxPona.ttf)');
    await SitelenPona$.load()  
    document.fonts.add(SitelenPona$)
    if(typeof(main)!="undefined"){
        main()
    }
}