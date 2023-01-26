#Luis Medina -
# Update the diameter of Lens Cap Holder and save each version as STL

import adsk.core, adsk.fusion, adsk.cam, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = adsk.fusion.Design.cast(app.activeProduct)

        defaultInputMinDiam = '35'
        minLensDiam_Input = ui.inputBox('Input diameter in mm: ', 
                                'Define minimum diameter', defaultInputMinDiam)

        defaultInputMaxDiam = '80'
        maxLensDiam_Input = ui.inputBox('Input diameter in mm: ', 
                                'Define maximum diameter', defaultInputMaxDiam)

        defaultInputWidth = '35'
        StrapWidth_Input = ui.inputBox('Input width in mm: ', 
                                'Define strap width', defaultInputWidth)
        ui.messageBox(f'Input is = {StrapWidth_Input[0]}')

        defaultInputFolder = r'C:\\'
        folderInput = ui.inputBox('Input path to save folder: ', 
        'Define Save Folder', defaultInputFolder)

        folder = folderInput[0]
                
        diameters = list(range(int(minLensDiam_Input[0])-1,int(maxLensDiam_Input[0])+1,1))
        
        # Get the root component of the active design
        rootComp = design.rootComponent

        # Get the parameters named "Length" and "Width" to change.
        LensDiam_par = design.allParameters.itemByName('LensDiam')
        StrapWidth_par = design.allParameters.itemByName('StrapWidth')

        for dim in diameters:
       
            Diam_set = dim
            Width_set = StrapWidth_Input[0]
            LensDiam_par.expression = str(Diam_set)
            StrapWidth_par.expression = str(Width_set)

            # Let the view have a chance to paint just so you can watch the progress.
            adsk.doEvents()
            
            # Construct the output filename.
            filename = f'{folder}\LensCapHolder_D{Diam_set}mm_Strap_{Width_set}mm.stl'
            
            # Save the file as STL.
            exportMgr = adsk.fusion.ExportManager.cast(design.exportManager)
            stlOptions = exportMgr.createSTLExportOptions(rootComp)
            stlOptions.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementMedium
            stlOptions.filename = filename
            exportMgr.execute(stlOptions)
        
        ui.messageBox('Finished.')
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
