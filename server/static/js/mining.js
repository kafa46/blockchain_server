$(function(){
    // 코인 amount 요청
    $('#query_coin_status').on('click', function(e){
        reload_amount();
    });

    

    // $('#query_coin_status').on('click', function(e){
    //     // e.preventDefault();
    //     let decision = confirm('입력한 지갑주소의 코인을 조회하시겠습니까?');
    //     if (decision == true){
    //         // let send_string = $('#blockchain_addr_input').val()
    //         let blockchain_addr = $('#blockchain_addr_input').val()
    //         let send_data = {'blockchain_addr': blockchain_addr}
    //         $.ajax({
    //             url: "/coin_amount",
    //             type: 'post',
    //             data: JSON.stringify(send_data),
    //             contentType: "application/json",
    //             dataType: 'json',
    //             success: function(response){
    //                 if (response.status == 'fail'){
    //                     alert(response.content)
    //                 }
    //                 if (response.status == 'success'){
    //                     // alert('조회에 성공했습니다.')
    //                     $('#current_coin_amount').val(response.content)
    //                 }
    //             },
    //             error: function(error){
    //                 alert('에러가 발생했어요 ㅠㅠ', error)
    //             }
    //         });
    //     }
    // });

    $('#start_mining').on('click', function(e){
        // e.preventDefault();
        let blockchain_addr = $('#blockchain_addr_input').val()
        let send_data = {'blockchain_addr': blockchain_addr}
        console.log(blockchain_addr)
        alert('채굴하는 동안에는 컴퓨터가 항상 켜져 있어야 합니다 ^^. \n채굴을 시작할까요?', send_data)
        $.ajax({
            url: '/mining/',
            type: 'post',
            data: JSON.stringify(send_data),
            contentType: 'application/json',
            dataType: 'json',
            success: function(response){
                if (response.status == 'success'){
                    alert('채굴에 성공했습니다.')
                    $('#current_coin_amount').val(response.reason)
                }
                if (response.status == 'fail'){
                    alert(response.reason)
                }

            },
            error: function(error){
                alert('에러가 발생했어요 ㅠㅠ', error)
            }
        });
    });
});

function reload_amount(){
    let decision = confirm('입력한 지갑주소의 코인을 조회하시겠습니까?');
    if (decision == true){
        // let send_string = $('#blockchain_addr_input').val()
        let blockchain_addr = $('#blockchain_addr_input').val()
        let send_data = {'blockchain_addr': blockchain_addr}
        $.ajax({
            url: "/coin_amount",
            type: 'post',
            data: JSON.stringify(send_data),
            contentType: "application/json",
            dataType: 'json',
            success: function(response){
                if (response.status == 'fail'){
                    alert(response.content)
                }
                if (response.status == 'success'){
                    // alert('조회에 성공했습니다.')
                    $('#current_coin_amount').val(response.content)
                }
            },
            error: function(error){
                alert('에러가 발생했어요 ㅠㅠ', error)
            }
        });
    }
}