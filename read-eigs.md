#------------------------------------------------------------------------------
# Print read colorvec eigeninfo
#
proc print_read_single_lime_colorvec
{
  local($local_path,$input) = @_

  # 
  open(INPUT, ">> $input")
  print INPUT <<EOF
    <elem>
      <Name>QIO_READ_NAMED_OBJECT</Name>
      <Frequency>1</Frequency>
      <NamedObject>
        <object_id>eigeninfo_0</object_id>
        <object_type>SubsetVectorsLatticeColorVector</object_type>
        <MapObject>
          <MapObjType>MAP_OBJECT_MEMORY</MapObjType>
        </MapObject>
      </NamedObject>
      <File>
        <file_name>${local_path}</file_name>
      </File>
    </elem>
EOF
close(INPUT)
}


#------------------------------------------------------------------------------
# Print read single colorvec eigeninfo
#
proc print_read_subset_vectors
{
  local($single_file,$input) = @_

  # 
  open(INPUT, ">> $input")
  print INPUT <<EOF
    <elem>
      <Name>READ_SUBSET_VECTORS</Name>
      <File>
        <file_name>${single_file}</file_name>
      </File>
      <NamedObject>
        <object_id>eigeninfo_0</object_id>
      </NamedObject>
    </elem>
EOF
close(INPUT)
}
