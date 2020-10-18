// for test


<template>
  <div id="test">
    <el-divider></el-divider>
    <upload-excel></upload-excel>
    <el-divider></el-divider>
    <download-file></download-file>
  </div>
</template>

<script>
import uploadExcel from "@/components/uploadExcel";
import downloadFile from "@/components/downloadFile";

export default {
  name: 'Test',
  components: {
    uploadExcel,
    downloadFile
  }
}
</script>
