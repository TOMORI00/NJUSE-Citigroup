<template>
    <div class="div-heading-2">
        <el-header class="homepage-header" height="100px">
            <div class="div-logo">
                <a @click="toHomepage">
                    <img class="logo-img" src="../assets/nju.png">
                </a>
            </div>
            <div class="div-more-link">
                <div class="link-text">
                    <a @click="toAbout">
                        <h2>关于</h2>
                    </a>
                </div>
            </div>
        </el-header>
        <div class="title">公募基金/理财复现与顾问组合系统（EPC）</div>
        <el-divider></el-divider>
    </div>

</template>

<script>
    export default {
        name: "Heading_1",
        methods:{
            toHomepage(){
                this.$router.push('homepage')
            },
            toAbout(){
                this.$router.push('/about')
            }
        }
    }
</script>

<style scoped>
    .div-heading-2 {
        margin: auto;
        width: 90%;
        /*box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);*/
    }

    .div-logo {
        width: 160px;
        height: 160px;
        display: inline-block;
        position: relative;
        top: 10px;
        left: -475px;
    }

    .title {
        border-radius: 12px;
        box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.3);
        width: 800px;
        height: 60px;
        background: rgba(0, 0, 0, 0.1);
        margin-top: 25px;
        margin-left: auto;
        margin-right: auto;
        font-weight: bold;
        font-size: 40px;
    }

    .div-more-link {
        width: 150px;
        height: 30px;
        margin: auto;
        position: relative;
        top: 30px;
        right: -450px;
        display: inline-block;
    }

    .logo-img {
        margin: auto;
        width: 131.58px;
        height: 164.74px;
        position: relative;
        top: 15px;
    }

    .link-text {
        display: inline-block;
        border-radius: 15px;
        box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
        width: 80px;
        height: 30px;
        background: rgba(255, 254, 254, 0.4);
        margin-top: 25px;
        margin-left: auto;
        margin-right: auto;
    }
</style>